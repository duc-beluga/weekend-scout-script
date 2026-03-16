from nova_act import NovaAct
from urllib.parse import quote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import os

NOVA_ACT_API_KEY = os.environ.get("NOVA_ACT_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    location: str

def search_restaurant(encoded: str, result: dict):
    with NovaAct(
        starting_page=f"https://www.yelp.com/search?find_desc=restaurants&find_loc={encoded}&attrs=GoodForLunchDeals,cheap",
        nova_act_api_key=NOVA_ACT_API_KEY,
    ) as nova:
        nova.act(
            "From the list, click on a random restaurant with rating above 4.0.",
        )
        r = nova.act_get(
            "Summarize the current page and why it's a good restaurant option in 1 sentence. "
            "Tell me about its uniqueness, not its logistic like offer take out and has ... reviews.",
        )
        result["restaurant"] = r.response

def search_trail(user_pref: str, result: dict):
    with NovaAct(
        starting_page=f"https://www.alltrails.com/",
        nova_act_api_key=NOVA_ACT_API_KEY,
    ) as nova:
        nova.act(f"Find a hiking trail near {user_pref} using search box. "
                 f"After finished typing, click the top suggestion if it matches with {user_pref}")
        nova.act("Click on the one with good review (above 4.0)")
        h = nova.act_get(
            "Summarize the page and what makes this trail special? 1 sentence, no logistics.",
        )
        result["hiking"] = h.response

@app.post("/plan")
def plan(req: PlanRequest):
    encoded = quote(req.location)
    result = {}

    t1 = threading.Thread(target=search_restaurant, args=(encoded, result))
    t2 = threading.Thread(target=search_trail, args=(req.location, result))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    origin = quote(result["restaurant"])
    dest = quote(result["hiking"])
    with NovaAct(
        starting_page=f"https://www.google.com/maps/dir/{origin}/{dest}",
        nova_act_api_key=NOVA_ACT_API_KEY
    ) as nova:
        distance = nova.act_get(
            "What is the driving distance and time?",
        ).response
        result["distance"] = distance

    return {
        "restaurant_summary": result["restaurant"],
        "trail_summary": result["hiking"],
        "distance_btw_res_and_trail": result["distance"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}