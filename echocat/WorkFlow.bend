def adaptive_workflow(input: Union[Text, Audio]):
  bend match:
    case Audio(voice) when voice.emotion > 0.7:
      priority = HIGH
      route_to(voice_enhancer_gpu_group)
    case Text(msg) when contains(msg, "sad"):
      trigger_comfort_response()
      parallel: [update_mood_db(), notify_diary_service()]