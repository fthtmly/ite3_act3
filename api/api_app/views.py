from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

items = [
    {"id": 1, "name": "Hirono", "price": 20000},
    {"id": 2, "name": "Skull Panda", "price": 40000},
    {"id": 3, "name": "Labubu", "price": 30000},
    {"id": 4, "name": "Sonny Angel", "price": 50000},
]

def get_next_id():
    return max(item["id"] for item in items) + 1 if items else 1

def get_items(request):
    search_query = request.GET.get("search", "").lower()
    if search_query:
        filtered_items = [item for item in items if search_query in item["name"].lower()]
        return JsonResponse({"items": filtered_items})
    return JsonResponse({"items": items})

def get_item(request, item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return JsonResponse(item)
    return JsonResponse({"error": "Item not found"}, status=404)

@csrf_exempt
def add_item(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_item = {"id": get_next_id(), "name": data["name"], "price": data["price"]}
            items.append(new_item)
            return JsonResponse(new_item, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data"}, status=400)

@csrf_exempt
def update_item(request, item_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            for item in items:
                if item["id"] == item_id:
                    item["name"] = data.get("name", item["name"])
                    item["price"] = data.get("price", item["price"])
                    return JsonResponse(item)
            return JsonResponse({"error": "Item not found"}, status=404)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data"}, status=400)

@csrf_exempt
def delete_item(request, item_id):
    global items
    if request.method == "DELETE":
        if any(item["id"] == item_id for item in items):
            items = [item for item in items if item["id"] != item_id]
            return JsonResponse({"message": "Item deleted"}, status=200)
        return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)
