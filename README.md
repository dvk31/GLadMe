# open-dj6

`open-dj6` is a small open-source Django template that keeps the useful shape of the larger
MinuteWork stack without bringing along the platform complexity.

It includes:

- Django with a reusable `BaseModel` split into focused abstract classes
- A simple `SoftDeleteMixin`
- Lightweight service contracts built with an ABC, a Protocol, and a registry decorator
- React + Inertia + Vite wired directly into Django
- A minimal `OpenRouterGateway` plus an example `manage.py ai_chat` command

It intentionally leaves out:

- Multi-tenant middleware and scoped managers
- ACL and URN systems
- Billing-aware AI usage logging
- Celery, Channels, Temporal, and background orchestration
- Runtime contract enforcement decorators like `must_check` and `must_emit`
- Large shell bootstrapping, analytics, and app registries

## Quick Start

3. Install Python dependencies with poetry.

```bash
poetry install
```

2. Install frontend dependencies.

```bash
npm install
```

3. Create your local environment file.

```bash
cp .env.example .env
```

4. Run migrations.

```bash
./runstack migrate
```

5. Start Django and Vite in separate terminals.

```bash
./runstack runserver
```

```bash
npm run dev
```

6. Open `http://localhost:8000`.

## Template Shape

```text
open-dj6/
  config/                  Django settings and URL config
  common/models/           Base models and mixins
  common/services/         Base gateway, Protocol contract, registry
  ai/                      OpenRouter gateway and example command
  web/                     Example app, model, and Inertia view
  templates/               Base Django layout for Inertia
  frontend/                React entrypoint, pages, and styles
  tests/                   Pytest suite for the reusable seams
```

## Example OpenRouter Command

Once `OPENROUTER_API_KEY` is set:

```bash
./runstack ai_chat "Give me a short release note for this project."
```

Optional flags:

- `--system-prompt`
- `--model`
- `--temperature`
- `--max-tokens`

## Extension Notes

Keep the starter understandable by adding complexity only where it pays for itself.

- Add your own domain models by subclassing `BaseModel` or `SoftDeleteMixin, BaseModel`.
- Keep service interfaces narrow. If a provider only needs `chat_messages()`, do not add a broad
  platform abstraction around it.
- If you need a custom user model, set `AUTH_USER_MODEL` and the audit fields will follow it.
- If you later add more AI providers, register them through `common.services.registry`.

## Testing

Run the backend test suite with:

```bash
pytest
```
