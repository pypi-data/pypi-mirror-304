from typing import Optional, List
from pydantic import BaseModel, Field,  HttpUrl
from enum import Enum



class OrgRole(str, Enum):
    admin   = 'admin'
    member  = 'member'
    service = 'service'
    view    = 'view'
    

class OrgPostRequest(BaseModel):
    name:        str           = Field(min_length=1, max_length=39, description='Unique name for this org.')
    description: Optional[str] = Field(default=None, description='Optional user supplied description.')

class OrgPatchRequest(BaseModel):
    name:        Optional[str] = Field(max_length=39, description='Unique name for this org.')
    description: Optional[str] = Field(max_length=255, description='Optional user supplied description.')

class OrgMemberPostRequest(BaseModel):
    email:  str          = Field(description='The user_id of a member to invite to the org.')
    role:   OrgRole      = Field(description='The users role in the org')

class OrgMember(BaseModel):
    id:                  int      = Field(description="Unique membership id")
    name:                str      = Field(description="Member name")
    email:               str      = Field(description="Member email")    
    created_at:          float    = Field(description='The epoch timestamp when the membership was created.')
    updated_at:          float    = Field(description='The epoch timestamp when the membership was updated.')
    invited_by_name:     str      = Field(description="The name that invited this member to the org.")
    role:                OrgRole  = Field(description="The user's role in the org")
    accepted:            bool     = Field(description='True if the user has accepted the org membership.')
    


class Org(BaseModel):
    id:                  int           = Field(escription="Internal org id")
    name:                str           = Field(max_length=39, description='Unique name for this org.')
    description:         Optional[str] = Field(max_length=255, description='Optional user supplied description.')
    created_at:          float         = Field(description='The epoch timestamp when the org was created.')
    updated_at:          float         = Field(description='The epoch timestamp when the org was updated.')
    created_by:          Optional[int] = Field(description='The user_id of the user that created the org.')
    subscription_id:     str           = Field(description='The subscription_id for the org.')    
    gpt4_credits:        int           = Field(description='The number of GPT-4 message credits currently available to the org users for chat.jiggy.ai.')
    gpt3_5_credits:      int           = Field(description='The number of GPT-3 message credits currently available to the org users for chat.jiggy.ai.')
    subscription_status: str           = Field(description='The stripe subscription status.')
     
