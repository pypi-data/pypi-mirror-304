from deep_translator import GoogleTranslator
from langdetect import detect
from blikon_sdk.v2.models.sdk_configuration_model import SDKConfiguration
from blikon_sdk.v2.core.core import Core
from blikon_sdk.v2.services.log_service import LogService


def msg(text: str) -> str:
    sdk_configuration: SDKConfiguration = Core.get_sdk_configuration()
    log_service: LogService = Core.get_log_service()
    app_language = sdk_configuration.sdk_settings.client_application_language
    traduccion: str = text

    try:
        # Detect the language automatically
        detected_language = detect(text)

        log_service.info(
            f"Starting translation from language '{detected_language}' to '{app_language}'",
            text_to_translate=text,
            source="blikon_sdk",
            file_name="msg_helper.py",
            function_name="msg"
        )

        # Translate only if detected language differs from app client language
        if detected_language != app_language:
            translator = GoogleTranslator(source=detected_language, target=app_language)
            result = translator.translate(text)
            traduccion = result

    except Exception as e:
        log_service.error(
            f"Unable to translate to '{app_language}' language",
            error_message=str(e),
            text_to_translate=text,
            source="blikon_sdk",
            file_name="msg_helper.py",
            function_name="msg"
        )

    return traduccion