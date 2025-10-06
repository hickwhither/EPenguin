- `POST /signin` - Đăng nhập bằng username/password
- `POST /logout` - Đăng xuất (login required)
- `GET /profile` - Lấy thông tin profile của user hiện tại (login required)

Flask-Login tạo cookie session (ví dụ: session hoặc sessionid) sau khi đăng nhập thành công (/signin).
```js
fetch("https://api.backend.com/signin", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username, password }),
  credentials: "include"  // BẮT BUỘC để gửi cookie
});
```

---

## `POST /signin`
- `200` - `{"msg": "success}`
* `401` - `{"msg": "Wrong email or password"}`: khi username hoặc password thiếu, user không tồn tại, hoặc mật khẩu sai.

---

## `POST /logout`
- `200` - `{"msg": "success"}`
- `401 (unauthorized)` - nếu chưa login

---

## `GET /profile`

**Response 200**
```json
{
  "id": "user_doc_id",
  "username": "tên_user",
  "avatar": "url/avatar.jpg",
  "nickname": "biệt danh",
  "rating": 1500 // rating cho solo cac thu
}
```

- `401 (unauthorized)` -  chưa login
- `404` - `{"msg": "User not found"}`: chắc là vừa bị xóa acc á.

---

## Ví dụ curl

```bash
curl -X POST http://hi.hw.io.vn:5000/signin \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}'
```

```bash
curl -X GET http://hi.hw.io.vn:5000/profile \
  -b "session-cookie=..."
```


```bash
curl -X POST http://hi.hw.io.vn:5000/logout \
  -b "session-cookie=..."
```
