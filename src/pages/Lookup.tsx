import PageBreadcrumb from "../components/common/PageBreadCrumb";
import { useState } from "react";
import PageMeta from "../components/common/PageMeta";
import ComponentCard from "../components/common/ComponentCard";
import Label from "../components/form/Label.tsx";
import Input from "../components/form/input/InputField";
import Select from "../components/form/Select.tsx";
import Button from "../components/ui/button/Button";

export default function Lookup() {

  const [query, setQuery] = useState({
    "loc": "",
    "div": "",
    "month": "",
    "type": "",
  });

  const [div_ops, setDivOptions] = useState<{ value: string; label: string; }[]>([])

  // const [topic_ops, setTopicOptions] = useState<{ value: string; label: string; }[]>([])

  const loc_ops = [
    { value: "reg", label: "Regional" },
    { value: "sw", label: "Statewide" },
    { value: "states", label: "States" },
    { value: "nats", label: "Nationals" },
    { value: "other", label: "Other" },
  ];

  const div_ops_local = [
    { value: "geo", label: "Geometry" },
    { value: "alg2", label: "Algebra 2" },
    { value: "precalc", label: "Precalculus" },
    { value: "stats", label: "Statistics" },
    { value: "calc", label: "Calculus" },
    { value: "misc", label: "Opens/Misc." },
  ];

  const div_ops_non_local = [
    { value: "theta", label: "Theta" },
    { value: "alpha", label: "Alpha" },
    { value: "stats", label: "Statistics" },
    { value: "mu", label: "Mu" },
    { value: "misc", label: "Opens/Misc." },
  ]

  const month_ops = [
    { value: "jan", label: "January" },
    { value: "feb", label: "February" },
    { value: "mar", label: "March" },
  ];

  const type_ops = [
    { value: "indiv", label: "Individual" },
    { value: "cipher", label: "Ciphering" },
    { value: "bowl", label: "Bowl" },
    { value: "topics", label: "Topic Tests" },
    { value: "other", label: "Other" },
  ];

  const handleSelectChange = (value: string) => {
    console.log("Selected value:", value);

    // disable month if loc_ops is state or nats
    // if states or nats, switch div ops to non local, if not, do local

    // add values to query dict then
    // if the new value is within like the loc ops then add make that the new query loc, etc.

    setQuery(prevQuery => {
      const query = { ...prevQuery }

      if (loc_ops.some(e => e.value == value)) {
        query["loc"] = value
        if (value == "reg" || value == "sw") {
          setDivOptions(div_ops_local)
          query["month"] = ""
        } else {
          setDivOptions(div_ops_non_local)
        }

        query["div"] = "";

      } else if (div_ops.some(e => e.value == value)) {
        query["div"] = value
      } else if (month_ops.some(e => e.value == value)) {
        query["month"] = value
      } else if (type_ops.some(e => e.value == value)) {
        query["type"] = value
      }
      return query;
    })
  };

  const [response, setResponse] = useState(null);

  const handleSubmit = async () => {
    const message = Object.entries(query)
      .filter(([_, value]) => value)
      .map(([key, value]) => `${key}: ${value}`)
      .join(", ");


    const dataToSend = { message }; // Whatever you want to send

    const res = await fetch("http://localhost:3001/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    });

    const result = await res.json();
    setResponse(result);
  };
  
  return (
    <div>
      <PageMeta
        title="Lookup"
        description="famat lookup + trainer bc i am lazy lol"
      />
      <PageBreadcrumb pageTitle="Lookup" />
      <div className="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12">
        <div className="mx-auto w-full max-w-[630px] text-center">
          <h3 className="mb-4 font-semibold text-gray-800 text-theme-xl dark:text-white/90 sm:text-2xl">
            Database Lookup
          </h3>

          <ComponentCard title="Enter test/question details:">

              <div className="flex flex-wrap items-center justify-center gap-8">
                <div>
                  <Label>Competition:</Label>
                  <Select
                    options={loc_ops}
                    placeholder="Select Option"
                    onChange={handleSelectChange}
                    className="dark:bg-dark-900"
                  />
                </div>


                <div>
                  <Label>Division:</Label>
                  <Select
                    options={div_ops}
                    placeholder="Select Option"
                    onChange={handleSelectChange}
                    className="dark:bg-dark-900"
                  />
                </div>

                <div>
                  <Label>Month:</Label>
                  <Select
                    options={month_ops}
                    placeholder="Select Option"
                    onChange={handleSelectChange}
                    className="dark:bg-dark-900"
                    disabled={!(query.loc == "reg" || query.loc == "sw")}
                  />
                </div>

                <div>
                  <Label>Type of Test:</Label>
                  <Select
                    options={type_ops}
                    placeholder="Select Option"
                    onChange={handleSelectChange}
                    className="dark:bg-dark-900"
                  />
                </div>

                <div>
                  <Label>Topic:</Label>
                  <Select
                    options={type_ops}
                    placeholder="Select Option"
                    onChange={handleSelectChange}
                    className="dark:bg-dark-900"
                    disabled={!(query.loc == "states" || query.loc == "nats")}
                  />
                </div>
              
                <div>
                  <Label htmlFor="input">Year:</Label>
                  <Input type="text" id="input" />
                </div>

              </div>
              <Button size="md" variant="primary" onClick={handleSubmit}>
                Submit Query
              </Button>
              {response && <pre>{JSON.stringify(response, null, 2)}</pre>}

          </ComponentCard>
        </div>
      </div>
    </div>
  );
}
