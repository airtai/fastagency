import React from 'react';
import ModelItem, { ItemProps } from './ModelItem';

interface ModelListProps {
  models: ItemProps[] | undefined;
  onSelectModel: (index: number) => void;
  type_name: string;
}

const ModelsList: React.FC<ModelListProps> = ({ models, onSelectModel, type_name }) => {
  if (!models || models.length === 0) {
    return (
      <div className='flex flex-col gap-3'>
        {/* <h2 className='text-lg font-semibold text-airt-primary'>Available Models</h2> */}
        <p className='text-airt-primary mt-1 -mt-3 opacity-50'>{`No ${type_name}s found. Please add one.`}</p>
      </div>
    );
  }

  return (
    <div className='flex flex-col gap-3'>
      {/* <h2 className='text-lg font-semibold text-airt-primary'>Available Models</h2> */}
      <div className='grid grid-cols-1 mx:auto md:grid-cols-2 lg:grid-cols-3 gap-3'>
        {models.map((model, index) => (
          <ModelItem key={index} model={model} onClick={() => onSelectModel(index)} />
        ))}
      </div>
    </div>
  );
};

export default ModelsList;
