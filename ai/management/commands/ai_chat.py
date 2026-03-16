"""Example management command for the OpenRouter gateway."""

from django.core.management.base import BaseCommand, CommandError

from ai.openrouter_gateway import OpenRouterGateway


class Command(BaseCommand):
    help = "Send a prompt to OpenRouter and print the response."

    def add_arguments(self, parser) -> None:
        parser.add_argument("prompt", help="Prompt to send to OpenRouter.")
        parser.add_argument(
            "--system-prompt",
            default=None,
            help="Optional system message.",
        )
        parser.add_argument(
            "--model",
            default=None,
            help="Override the configured default model.",
        )
        parser.add_argument(
            "--temperature",
            type=float,
            default=None,
            help="Sampling temperature override.",
        )
        parser.add_argument(
            "--max-tokens",
            type=int,
            default=1200,
            help="Maximum response tokens.",
        )

    def handle(self, *args, **options) -> None:
        gateway = OpenRouterGateway()
        if not gateway.is_configured():
            raise CommandError(
                "OPENROUTER_API_KEY is not set. Copy .env.example to .env and add a key first."
            )

        response = gateway.chat(
            options["prompt"],
            system_prompt=options["system_prompt"],
            model=options["model"],
            temperature=options["temperature"],
            max_tokens=options["max_tokens"],
        )
        self.stdout.write(response)

        if gateway.last_usage is not None:
            self.stderr.write(
                self.style.NOTICE(
                    "usage: "
                    f"{gateway.last_usage.prompt_tokens} prompt / "
                    f"{gateway.last_usage.completion_tokens} completion / "
                    f"{gateway.last_usage.total_tokens} total"
                )
            )
