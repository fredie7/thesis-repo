import { getApps, getApp, initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCtU8JeL7mkcZJg_s43ThCaiR-9gy5d7nQ",
  authDomain: "cbt-db.firebaseapp.com",
  projectId: "cbt-db",
  storageBucket: "cbt-db.appspot.com",
  messagingSenderId: "4992102740",
  appId: "1:4992102740:web:4f302e553e17a6502c18c1",
};

// Initialize Firebase
const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };
