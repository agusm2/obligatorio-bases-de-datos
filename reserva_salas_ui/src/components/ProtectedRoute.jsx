import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function ProtectedRoute({ role, children }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to={"/"} />;
  }

  if (role && user.role != role) {
    return <Navigate to={"/"} />;
  }

  return children;
}
