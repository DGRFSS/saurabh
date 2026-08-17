import { useEffect } from "react";

function App() {
  useEffect(() => {
    window.location.replace("/master-chart.html");
  }, []);
  return null;
}

export default App;
