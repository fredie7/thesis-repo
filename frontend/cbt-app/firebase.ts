import { getApps, getApp, initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// const firebaseConfig = {
//   apiKey: "AIzaSyCtU8JeL7mkcZJg_s43ThCaiR-9gy5d7nQ",
//   authDomain: "cbt-db.firebaseapp.com",
//   projectId: "cbt-db",
//   storageBucket: "cbt-db.appspot.com",
//   messagingSenderId: "4992102740",
//   appId: "1:4992102740:web:4f302e553e17a6502c18c1",
// };
const firebaseConfig = {
  apiKey: "AIzaSyC2A92ljj-JkQS1de9K9U3i9n9wOsWrBgg",
  authDomain: "cdd-db-d9a47.firebaseapp.com",
  projectId: "cdd-db-d9a47",
  storageBucket: "cdd-db-d9a47.appspot.com",
  messagingSenderId: "914595994855",
  appId: "1:914595994855:web:cfb4ee43f86ce9a6d4d642",
};
// Initialize Firebase
const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };
