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
- {"msg": "success"}
- 401: nếu chưa login

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

- `404` - `{"msg": "User not found"}`: nếu `current_user.is_active` là False hoặc user không tồn tại.

---

## Ví dụ curl


```bash
curl -X POST https://yourdomain.com/signin \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}'
```

```bash
curl -X GET https://yourdomain.com/profile \
  -b "session-cookie=..."
```


```bash
curl -X POST https://yourdomain.com/logout \
  -b "session-cookie=..."
```
