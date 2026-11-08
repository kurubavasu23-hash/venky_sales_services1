import axios from 'axios';
export const business={name:'Venky Mobiles Sales & Services',phone:'+91 8555077760',whatsappNumber:'918555077760',address:'Near Clock Tower, Uravakonda, Andhra Pradesh, India',hours:'Every day, 9:00 AM to 9:00 PM',phoneLink:'tel:+918555077760',whatsapp:'https://wa.me/918555077760',mapsLink:'https://maps.app.goo.gl/yjfwT9eYAZNju1ZN9'};
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api',timeout:10000,headers:{'Content-Type':'application/json'}});
