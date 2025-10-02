import { BrowserRouter as Router, Routes, Route } from "react-router";
import NotFound from "./pages/OtherPage/NotFound";
import Homepage from "./pages/Homepage";
import Lookup from "./pages/Lookup";
import AppLayout from "./layout/AppLayout";
import { ScrollToTop } from "./components/common/ScrollToTop";
// import FormElements from "./pages/Forms/FormElements";
import Buttons from "./pages/UiElements/Buttons";

export default function App() {
  return (
    <>
      <Router>
        <ScrollToTop />
        <Routes>
          {/* Dashboard Layout */}
          <Route element={<AppLayout />}>
            <Route index path="/" element={<Homepage />} />

            <Route path="/lookup" element={<Lookup />} />

            {/* <Route path="/trainer" element={<Trainer />} /> */}
          </Route>

          {/* Forms */}
          {/* <Route path="/form-elements" element={<FormElements />} /> */}

          <Route path="/buttons" element={<Buttons />} />

          {/* Fallback Route */}
          <Route path="*" element={<NotFound />} />
          
        </Routes>
      </Router>
    </>
  );
}
