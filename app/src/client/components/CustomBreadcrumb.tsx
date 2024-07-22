import { Link } from 'react-router-dom';
interface BreadcrumbProps {
  pageName: string;
}
const CustomBreadcrumb = ({ pageName }: BreadcrumbProps) => {
  return (
    <div className='mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between'>
      <h2 className='text-title-md2 font-semibold text-airt-primary dark:text-white'>{pageName}</h2>

      {/* <nav>
        <ol className='flex items-center gap-2'>
          <li>
            <Link className='text-airt-font-base' to='/build'>
              Build /
            </Link>
          </li>
          <li className='text-airt-secondary'>{pageName}</li>
        </ol>
      </nav> */}
    </div>
  );
};

export default CustomBreadcrumb;
