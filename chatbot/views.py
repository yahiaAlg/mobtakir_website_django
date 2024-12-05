from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import ChatSession, ChatMessage
import ollama
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.schema import HumanMessage, SystemMessage
from django.contrib import messages

@login_required
def chat_view(request):
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        prompt = request.POST.get("prompt")

        # Get or create chat session
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(
                user=request.user,
                title=prompt[:50],  # Use first 50 chars of first message as title
            )

        # Save user message
        ChatMessage.objects.create(session=session, role="user", content=prompt)

        try:
            response_content = ""

            # Check which model to use based on session settings
            if "gemini" in session.model_name.lower():
                # Initialize Google's Gemini model
                chat = ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    google_api_key=os.getenv("GOOGLE_API_KEY"),
                    temperature=0.7,
                )

                # Get chat history for context
                messages = []
                history = session.messages.all().order_by("timestamp")[
                    :5
                ]  # Last 5 messages
                for msg in history:
                    if msg.role == "user":
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role == "assistant":
                        messages.append(SystemMessage(content=msg.content))

                # Add current prompt
                messages.append(HumanMessage(content=prompt))

                # Get response from Gemini
                response = chat.invoke(messages)
                response_content = response.content

            else:  # Use Ollama model
                model_name = session.model_name if session.model_name else "phi3"

                # Get response from Ollama
                response = ollama.chat(
                    model=model_name, messages=[{"role": "user", "content": prompt}]
                )
                response_content = response["message"]["content"]

            # Save assistant response
            assistant_message = ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=response_content,
            )

            return JsonResponse(
                {
                    "content": assistant_message.content,
                    "timestamp": assistant_message.time_formatted,
                    "session_id": session.id,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e), "status": 400}, status=400)

    # GET request - render chat interface
    sessions = ChatSession.objects.filter(user=request.user)
    return render(request, "chatbot/chat_interface.html", {"sessions": sessions})


@login_required
def chat_history_view(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages = session.messages.all()
    return JsonResponse(
        {"messages": list(messages.values("role", "content", "timestamp"))}
    )


@login_required
def chat_sessions_view(request):
    sessions = ChatSession.objects.filter(user=request.user)
    return JsonResponse(
        {"sessions": list(sessions.values("id", "title", "created_at", "updated_at"))}
    )


@login_required
def chat_settings(request):
    if request.method == "POST":
        # Get settings from the form
        model_name = request.POST.get("language_model")
        temperature = float(request.POST.get("temperature", 0.7))
        max_length = int(request.POST.get("max_length", 500))
        context_memory = int(request.POST.get("context_memory", 5))
        language = request.POST.get("primary_language", "English")
        auto_correct = request.POST.get("auto_correct") == "on"
        api_key = request.POST.get("api_key", "")
        endpoint_url = request.POST.get("endpoint_url", "")

        # Map frontend model names to backend model names
        model_mapping = {
            "GPT-4": "gpt-4",
            "GPT-3.5": "gpt-3.5-turbo",
            "Claude": "claude-2",
            "Gemini": "gemini-pro",
            "Ollama": "orca-mini",
        }

        # Get the actual model name from mapping
        backend_model_name = model_mapping.get(model_name, "orca-mini")

        try:
            # Update or create default settings for the user
            session, created = ChatSession.objects.get_or_create(
                user=request.user,
                title="Default Settings",
                defaults={
                    "model_name": backend_model_name,
                },
            )

            if not created:
                session.model_name = backend_model_name
                session.save()

            # Store additional settings in session
            request.session["chat_settings"] = {
                "temperature": temperature,
                "max_length": max_length,
                "context_memory": context_memory,
                "language": language,
                "auto_correct": auto_correct,
                "api_key": api_key,  # Consider encrypting this
                "endpoint_url": endpoint_url,
            }

            messages.success(request, "Settings saved successfully!")
            return redirect("chatbot:chat")

        except Exception as e:
            messages.error(request, f"Error saving settings: {str(e)}")
            return redirect("chatbot:chat_settings")

    # GET request - load current settings
    try:
        default_session = ChatSession.objects.filter(
            user=request.user, title="Default Settings"
        ).first()

        # Reverse map model names for frontend
        reverse_model_mapping = {
            "gpt-4": "GPT-4",
            "gpt-3.5-turbo": "GPT-3.5",
            "claude-2": "Claude",
            "gemini-pro": "Gemini",
            "orca-mini": "Ollama",
        }

        current_settings = request.session.get("chat_settings", {})
        context = {
            "current_model": reverse_model_mapping.get(
                default_session.model_name if default_session else "orca-mini", "Ollama"
            ),
            "temperature": current_settings.get("temperature", 0.7),
            "max_length": current_settings.get("max_length", 500),
            "context_memory": current_settings.get("context_memory", 5),
            "language": current_settings.get("language", "English"),
            "auto_correct": current_settings.get("auto_correct", False),
            "api_key": current_settings.get("api_key", ""),
            "endpoint_url": current_settings.get("endpoint_url", ""),
        }

        return render(request, "chatbot/chat_settings.html", context)

    except Exception as e:
        messages.error(request, f"Error loading settings: {str(e)}")
        return redirect("chatbot:chat")


@login_required
def load_chat_settings(request):
    """Utility function to load chat settings for a session"""
    try:
        # Load default settings
        default_session = ChatSession.objects.filter(
            user=request.user, title="Default Settings"
        ).first()

        if default_session:
            current_settings = request.session.get("chat_settings", {})

            return JsonResponse(
                {
                    "success": True,
                    "settings": {
                        "model_name": default_session.model_name,
                        "temperature": current_settings.get("temperature", 0.7),
                        "max_length": current_settings.get("max_length", 500),
                        "context_memory": current_settings.get("context_memory", 5),
                        "language": current_settings.get("language", "English"),
                        "auto_correct": current_settings.get("auto_correct", False),
                        "api_key": current_settings.get("api_key", ""),
                        "endpoint_url": current_settings.get("endpoint_url", ""),
                    },
                }
            )
        else:
            return JsonResponse(
                {"success": False, "error": "No default settings found"}
            )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
