import axios from 'axios';
import { BASE_URL } from '../constants/Url';

export const axiosClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});