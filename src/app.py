"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from copy import deepcopy
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
import os
from pathlib import Path

app = FastAPI(title="Slalom Capabilities Management API",
              description="API for managing consulting capabilities and consultant expertise")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory capabilities database
capabilities = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,
        "consultant_emails": ["alice.smith@slalom.com", "bob.johnson@slalom.com"]
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology", 
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultant_emails": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"]
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"], 
        "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultant_emails": ["john.brown@slalom.com", "olivia.taylor@slalom.com"]
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultant_emails": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"]
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultant_emails": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"]
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultant_emails": ["amelia.lee@slalom.com", "harper.white@slalom.com"]
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultant_emails": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"]
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultant_emails": ["james.walker@slalom.com", "benjamin.hall@slalom.com"]
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultant_emails": ["charlotte.young@slalom.com", "henry.king@slalom.com"]
    }
}


class ConsultantBase(BaseModel):
    name: str
    email: EmailStr
    practice_area: str
    location: str
    bio: str
    contact_details: Optional[str] = None


class ConsultantCreate(ConsultantBase):
    pass


class ConsultantUpdate(BaseModel):
    name: Optional[str] = None
    practice_area: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    contact_details: Optional[str] = None


def build_profile(email: str, practice_area: str, location: str) -> Dict[str, Optional[str]]:
    first_name, last_name = email.split("@")[0].split(".")
    return {
        "name": f"{first_name.title()} {last_name.title()}",
        "email": email,
        "practice_area": practice_area,
        "location": location,
        "bio": f"{first_name.title()} supports {practice_area.lower()} engagements across Slalom accounts.",
        "contact_details": None,
    }


consultants = {
    "alice.smith@slalom.com": build_profile("alice.smith@slalom.com", "Technology", "Seattle, WA"),
    "bob.johnson@slalom.com": build_profile("bob.johnson@slalom.com", "Technology", "Chicago, IL"),
    "emma.davis@slalom.com": build_profile("emma.davis@slalom.com", "Technology", "Atlanta, GA"),
    "sophia.wilson@slalom.com": build_profile("sophia.wilson@slalom.com", "Technology", "Denver, CO"),
    "john.brown@slalom.com": build_profile("john.brown@slalom.com", "Technology", "Austin, TX"),
    "olivia.taylor@slalom.com": build_profile("olivia.taylor@slalom.com", "Technology", "Portland, OR"),
    "liam.anderson@slalom.com": build_profile("liam.anderson@slalom.com", "Strategy", "Boston, MA"),
    "noah.martinez@slalom.com": build_profile("noah.martinez@slalom.com", "Strategy", "New York, NY"),
    "ava.garcia@slalom.com": build_profile("ava.garcia@slalom.com", "Operations", "Dallas, TX"),
    "mia.rodriguez@slalom.com": build_profile("mia.rodriguez@slalom.com", "Operations", "Phoenix, AZ"),
    "amelia.lee@slalom.com": build_profile("amelia.lee@slalom.com", "Technology", "Los Angeles, CA"),
    "harper.white@slalom.com": build_profile("harper.white@slalom.com", "Technology", "San Francisco, CA"),
    "ella.clark@slalom.com": build_profile("ella.clark@slalom.com", "Technology", "Washington, DC"),
    "scarlett.lewis@slalom.com": build_profile("scarlett.lewis@slalom.com", "Technology", "Miami, FL"),
    "james.walker@slalom.com": build_profile("james.walker@slalom.com", "Technology", "Detroit, MI"),
    "benjamin.hall@slalom.com": build_profile("benjamin.hall@slalom.com", "Technology", "Minneapolis, MN"),
    "charlotte.young@slalom.com": build_profile("charlotte.young@slalom.com", "Operations", "Nashville, TN"),
    "henry.king@slalom.com": build_profile("henry.king@slalom.com", "Operations", "Columbus, OH"),
}


def consultant_payload(email: str) -> Dict[str, Optional[str]]:
    consultant = consultants.get(email)
    if consultant is None:
        raise HTTPException(status_code=500, detail=f"Consultant record missing for {email}")
    return deepcopy(consultant)


def capability_payload(name: str, details: Dict[str, object]) -> Dict[str, object]:
    payload = deepcopy(details)
    consultant_emails: List[str] = payload.pop("consultant_emails", [])
    payload["consultants"] = [consultant_payload(email) for email in consultant_emails]
    return payload


def ensure_consultant_exists(email: str) -> None:
    if email not in consultants:
        raise HTTPException(status_code=404, detail="Consultant not found")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return {
        capability_name: capability_payload(capability_name, details)
        for capability_name, details in capabilities.items()
    }


@app.get("/consultants")
def get_consultants():
    return sorted(
        (deepcopy(consultant) for consultant in consultants.values()),
        key=lambda consultant: consultant["name"],
    )


@app.get("/consultants/{email}")
def get_consultant(email: EmailStr):
    ensure_consultant_exists(str(email))
    return consultant_payload(str(email))


@app.post("/consultants", status_code=201)
def create_consultant(consultant: ConsultantCreate):
    email = str(consultant.email)
    if email in consultants:
        raise HTTPException(status_code=400, detail="Consultant already exists")

    consultants[email] = consultant.model_dump()
    return consultant_payload(email)


@app.put("/consultants/{email}")
def update_consultant(email: EmailStr, consultant_update: ConsultantUpdate):
    email_str = str(email)
    ensure_consultant_exists(email_str)

    updates = consultant_update.model_dump(exclude_unset=True)
    consultants[email_str].update(updates)
    return consultant_payload(email_str)


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str):
    """Register a consultant for a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    ensure_consultant_exists(email)

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is not already registered
    if email in capability["consultant_emails"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability"
        )

    # Add consultant
    capability["consultant_emails"].append(email)
    consultant = consultant_payload(email)
    return {"message": f"Registered {consultant['name']} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    ensure_consultant_exists(email)

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is registered
    if email not in capability["consultant_emails"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )

    # Remove consultant
    capability["consultant_emails"].remove(email)
    consultant = consultant_payload(email)
    return {"message": f"Unregistered {consultant['name']} from {capability_name}"}
