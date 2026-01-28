"""Inventory Item Routes."""
from flask import Blueprint, jsonify, request
from uuid import UUID

from src.infrastructure.database.session import get_db_context
from src.infrastructure.database.models.inventory_item_model import InventoryItemModel

inventory_item_bp = Blueprint("inventory_items", __name__, url_prefix="/api/v1/inventory-items")


@inventory_item_bp.route("/", methods=["GET"])
def list_inventory_items():
    """List inventory items with filters."""
    try:
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", 50, type=int)
        search = request.args.get("search")
        category = request.args.get("category")
        status = request.args.get("status")
        
        with get_db_context() as session:
            query = session.query(InventoryItemModel)
            
            if search:
                search_filter = f"%{search}%"
                query = query.filter(
                    InventoryItemModel.name.ilike(search_filter) |
                    InventoryItemModel.code.like(search_filter)
                )
            
            if category:
                query = query.filter(InventoryItemModel.category == category)
            
            if status:
                query = query.filter(InventoryItemModel.status == status)
            
            total = query.count()
            items = query.offset((page - 1) * page_size).limit(page_size).all()
            
            return jsonify({
                "data": [
                    {
                        "id": str(item.id),
                        "name": item.name,
                        "code": item.code,
                        "category": item.category,
                        "quantity": item.quantity,
                        "minQuantity": item.min_quantity,
                        "unit": item.unit,
                        "status": item.status,
                        "location": item.location,
                        "costPrice": item.cost_price,
                        "salePrice": item.sale_price,
                        "expirationDate": item.expiration_date.isoformat() if item.expiration_date else None,
                    }
                    for item in items
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "pageSize": page_size,
                    "totalPages": (total + page_size - 1) // page_size,
                }
            }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@inventory_item_bp.route("/<item_id>", methods=["GET"])
def get_inventory_item(item_id: str):
    """Get inventory item by ID."""
    try:
        with get_db_context() as session:
            item = session.query(InventoryItemModel).filter(
                InventoryItemModel.id == UUID(item_id)
            ).first()
            
            if not item:
                return jsonify({"error": "Item not found"}), 404
            
            return jsonify({
                "id": str(item.id),
                "name": item.name,
                "code": item.code,
                "barcode": item.barcode,
                "category": item.category,
                "description": item.description,
                "quantity": item.quantity,
                "minQuantity": item.min_quantity,
                "maxQuantity": item.max_quantity,
                "unit": item.unit,
                "status": item.status,
                "location": item.location,
                "batch": item.batch,
                "expirationDate": item.expiration_date.isoformat() if item.expiration_date else None,
                "supplier": item.supplier,
                "costPrice": item.cost_price,
                "salePrice": item.sale_price,
                "notes": item.notes,
                "createdAt": item.created_at.isoformat(),
                "updatedAt": item.updated_at.isoformat(),
            }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@inventory_item_bp.route("/low-stock", methods=["GET"])
def get_low_stock_items():
    """Get items with low stock."""
    try:
        with get_db_context() as session:
            items = session.query(InventoryItemModel).filter(
                InventoryItemModel.quantity <= InventoryItemModel.min_quantity
            ).limit(100).all()
            
            return jsonify({
                "data": [
                    {
                        "id": str(item.id),
                        "name": item.name,
                        "code": item.code,
                        "quantity": item.quantity,
                        "minQuantity": item.min_quantity,
                        "status": item.status,
                    }
                    for item in items
                ],
                "total": len(items),
            }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
