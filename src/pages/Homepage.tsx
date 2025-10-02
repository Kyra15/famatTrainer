import CardDataStats from "../components/ui/table/CardDataStats";
import { Link } from "react-router";
import {
  EyeIcon,
  PencilIcon
} from "../icons";

export default function Homepage() {
  return (
    <div>
      <div className="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12">
        <div className="mx-auto w-full max-w-[630px] text-center">
          <h3 className="mb-4 font-semibold text-gray-800 text-theme-xl dark:text-white/90 sm:text-2xl">
            FAMAT Lookup + Trainer
          </h3>

          <p className="text-sm text-gray-500 dark:text-gray-400 sm:text-base">
            famat lookup bc im lazy lol
          </p>
        </div>
        <br></br><br></br>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-2 2xl:gap-12">
          <Link to="/lookup">
            <CardDataStats title="Database" total="Lookup">
              <EyeIcon className="w-7 h-7 fill-brand-500 dark:fill-white"></EyeIcon>
            </CardDataStats>
          </Link>
          
          <Link to="/trainer">
            <CardDataStats title="Question" total="Trainer">
              <PencilIcon className="w-7 h-7 text-brand-500 dark:text-white"></PencilIcon>
            </CardDataStats>
          </Link>
        </div>
      </div>
    </div>
  );
}
