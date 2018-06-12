import axios from 'axios';

export const HTTP = axios.create({
  baseURL: `http://localhost:8000`,
  headers: {
    Authorization: 'Bearer {token}'
  }
});
 
export function getRooms() {
  return HTTP.get('rooms')
  .then(response => response)
  .catch(rerror => rerror);
  }

export function cube(x) {
  return x * x * x;
}