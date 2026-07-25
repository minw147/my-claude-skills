# Explore→Create switch requires explicit user intent

There is no UI to click a mode toggle — everything runs through conversation. The AI switches into Create Mode only when the user explicitly says so (e.g. "help me turn this into a video script"). The AI may make one gentle proposal if it observes a strong signal (highlight density, user enthusiasm), but never switches unprompted and never repeats the proposal if declined.

Considered: AI-detected intent switching (watching highlight accumulation and tone, then proactively offering/initiating Create Mode). Rejected because it risks the Khanmigo failure mode called out during competitive analysis — the AI deciding on the user's behalf what they need next erodes the "user fully controls how they learn" premise the whole product depends on. This is a product-philosophy line, not a convenience trade-off, so it's worth flagging clearly rather than letting a future contributor "helpfully" add auto-detection.
