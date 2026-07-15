from fastapi import APIRouter, HTTPException

from app.models.research_model import (
    ResearchRequest,
    ModifyRequest,
    VoiceRequest,
)

from app.services.research_service import research_service
from app.services.modify_service import modify_service
from app.services.voice_service import voice_service

router = APIRouter()


# ---------------------------------------------
# Home
# ---------------------------------------------

@router.get("/")
def home():

    return {
        "message": "AI Research Assistant API",
        "version": "2.0",
        "status": "running",
    }


# ---------------------------------------------
# Health
# ---------------------------------------------

@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ---------------------------------------------
# Research
# ---------------------------------------------

@router.post("/research")
def generate(request: ResearchRequest):

    try:

        report = research_service.generate_report(
            request.topic
        )

        return {
            "success": True,
            "topic": request.topic,
            "report": report,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------
# History
# ---------------------------------------------

@router.get("/history")
def history():

    return {
        "history":
        research_service.load_history()
    }


# ---------------------------------------------
# Delete History
# ---------------------------------------------

@router.delete("/history/{index}")
def delete(index: int):

    success = research_service.delete_history(
        index
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="History not found",
        )

    return {
        "success": True
    }


# ---------------------------------------------
# AI Report Editor
# ---------------------------------------------

@router.post("/edit-report")
def edit(request: ModifyRequest):

    try:

        edited = modify_service.modify_report(
            report=request.report,
            instruction=request.instruction,
        )

        return {
            "success": True,
            "report": edited,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------
# Voice Assistant
# ---------------------------------------------

@router.post("/voice")
def voice(request: VoiceRequest):

    try:

        response = voice_service.chat(
            request.prompt
        )

        return {
            "success": True,
            "response": response,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------
# Explain
# ---------------------------------------------

@router.post("/voice/explain")
def explain(request: VoiceRequest):

    try:

        response = voice_service.explain(
            request.prompt
        )

        return {
            "success": True,
            "response": response,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------
# Summarize
# ---------------------------------------------

@router.post("/voice/summarize")
def summarize(request: VoiceRequest):

    try:

        response = voice_service.summarize(
            request.prompt
        )

        return {
            "success": True,
            "response": response,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )