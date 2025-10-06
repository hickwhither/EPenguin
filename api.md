- `GET /api/problems` — Danh sách bài
- `GET /api/problem/<id>` — Lấy bài theo `id`.
- `GET /api/problem/<id>/update` — Gọi bot update bài. (không có ktra auth và chưa gắn delay đâu, ai spam cắchuym)

---

### `GET /api/problems`

**Query parameters**
- `page` — số trang (int). Default: `1`.
- `count` — số bài mỗi trang (int). Default: `20`.
- `oj` — lọc theo trường `oj` (luyencode, vnoi,...).
- `id` — lọc `id` dùng ilike (ilike là có chứa string con `id` trong đó)
- `title` — lọc `title` dùng ilike
- `rating_start` — lọc rating >= giá trị (int).
- `rating_end` — lọc rating <= giá trị (int).

**Response 200 JSON:**

```json
{
  "ojs": ["luyencode"],
  "pages": 12,
  "problems": [
    {
      "oj": "luyencode",
      "id": "luyencode_cb01",
      "link": "https://luyencode.net/problem/cb01",
      "updated_at": "6969", // int seconds passed since epoch
      "title": "Lập Trình Không Khó",
      "rating": null
    },
    ...
  ]
}
```

- `500` — `{"error": "invalid type <exception>"}`: tham số sai
- Không trả 404 nếu không có kết quả, `problems` là list rỗng và `pages` tối thiểu là 1

**Ví dụ CURL:**

```bash
curl "http://hi.hw.io.vn:5000/api/problems?page=2&count=10&rating_start=1200&rating_end=1800&title=graph"
```

---

### `GET /api/problem/<string:id>`

* `id` — id bài (string).

**Response 200 JSON**

```json
{
  "oj": "luyencode",
  "id": "luyencode_cb01",
  "link": "https://luyencode.net/problem/cb01",
  "updated_at": "6969", // int seconds passed since epoch
  "rating": null,
  "title": "Lập Trình Không Khó",
  "description": "Mô tả (HTML or text)", // coi chừng XSS attack, mà chắc k có đâu
  "translated": "Bản dịch tiếng Việt (nếu có)", // coi chừng XSS attack, mà chắc k có đâu
  "timelimit": "1s",
  "memorylimit": "256", // bằng MB
  "input": "file input hoặc stdin",
  "output": "file output hoặc stdout"
}
```

* `404` — `{"error": "Problem not exists"}`: nếu không tìm thấy bài toán với `id` đã cho.

---

### `GET /api/problem/<string:id>/update`
tạo scheduler để crawl bài đó, gọi `scheduler.add_job(...)` vô bot cho OJ đó

* `id` — id bài.

**Response 200 JSON:**

```json
{"success": "Job has been added"}
```

* `404` — `{"error": "Problem not exists"}`: không tìm thấy bài.
