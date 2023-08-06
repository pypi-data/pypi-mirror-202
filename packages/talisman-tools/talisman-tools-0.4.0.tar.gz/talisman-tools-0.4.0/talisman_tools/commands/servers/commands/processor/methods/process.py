import logging
from functools import partial
from logging import Logger
from operator import itemgetter
from typing import Any, List, Optional, Sequence, Tuple, Type, Union

from fastapi import FastAPI, HTTPException, Request
from tdm.json_schema import TalismanDocumentModel

from talisman_tools.commands.servers.server_helper import log_debug_data
from talisman_tools.helper.concurrency import execute_concurrently
from tp_interfaces.abstract import AbstractDocumentProcessor, ImmutableBaseModel
from tp_interfaces.helpers.batch import AbstractModelInput, batch_process_inputs
from tp_interfaces.logging.context import update_log_extras

_logger = logging.getLogger(__name__)


def register_process_docs(
        app: FastAPI,
        endpoint: str,
        processor: AbstractDocumentProcessor,
        document_model: Type[TalismanDocumentModel],
        logger: Logger = _logger
):
    config_model = processor.config_type

    class ModelInput(AbstractModelInput):
        message: document_model
        config: config_model

        def get_message(self) -> Any:
            return self.message

        def get_config(self) -> Optional[ImmutableBaseModel]:
            return self.config

    def process_with_config(messages: Sequence[TalismanDocumentModel], config: ImmutableBaseModel) \
            -> Tuple[TalismanDocumentModel, ...]:
        docs = tuple(message.to_doc() for message in messages)
        with update_log_extras(doc_id=[doc.doc_id for doc in docs]):
            output_docs = processor.process_docs(docs, config)
            return tuple(document_model.build(output_doc) for output_doc in output_docs)

    @app.post(endpoint, response_model=Union[List[TalismanDocumentModel], TalismanDocumentModel], response_model_exclude_none=True)
    async def process(request: Request, *, messages: Union[List[ModelInput], ModelInput]):
        response_post_processor = lambda x: x
        if not isinstance(messages, list):
            messages = [messages]
            response_post_processor = itemgetter(0)

        with update_log_extras(doc_id=[message.message.id for message in messages]):
            log_debug_data(logger, f"got {len(messages)} documents for processing", request)
            task = partial(batch_process_inputs, inputs=messages, processor=process_with_config)
            try:
                response = await execute_concurrently(task)
            except Exception as e:
                logger.error("Exception while processing request", exc_info=e)
                return HTTPException(status_code=500)
            log_debug_data(logger, f"processed {len(response)} documents", request)

            return response_post_processor(response)
