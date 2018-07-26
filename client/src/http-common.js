import axios from 'axios';

export const HTTP = axios.create({
  baseURL: `http://localhost:8000`,
  headers: {
    Authorization: 'Bearer {token}'
  }
});

export function getRooms(user_name) {
  if (user_name) {
    return HTTP.get('rooms',{params:{user_name:user_name}})
    .then(response => response)
    .catch(rerror => rerror);
  } else {
  return HTTP.get('rooms')
  .then(response => response)
  .catch(rerror => rerror);
  }
}

export function addUser(user_name) {
  return HTTP.post('user', user_name)
}
export function cube(x) {
  return x * x * x;
}