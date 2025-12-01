# Mock Weather API
Đây là một mock API đơn giản mô phỏng dữ liệu **thời tiết**.
Server được triển khai bằng **FastAPI**, chỉ hỗ trợ **GET endpoints**.

## 🚀 Chạy server

```bash
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload --host 0.0.0.0 --port 8067
```

## 📌 Endpoints

| Method | Path              | Mô tả                   |
| ------ | ----------------- | ----------------------- |
| GET    | `/health`         | Kiểm tra trạng thái API |
| GET    | `/weather/{city}` | Lấy thông tin thời tiết |

## 🔍 Ví dụ gọi API

```bash
curl http://localhost:8067/weather/hanoi
```

Kết quả mẫu:

```json
{
  "city": "hanoi",
  "temperature_c": 27.3,
  "condition": "Cloudy",
  "humidity": 70,
  "time": "2025-01-01T12:00:00Z"
}
```

## 📄 OpenAPI Spec

File đầy đủ nằm tại:

* `openapi.yaml`
* Hoặc tự động generate khi chạy server:

  * Swagger UI: [http://localhost:8067/docs](http://localhost:8067/docs)
  * OpenAPI JSON: [http://localhost:8067/openapi.json](http://localhost:8067/openapi.json)
