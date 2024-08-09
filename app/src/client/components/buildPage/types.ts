/* This file should be deleted */

export interface Props {
  data: any;
  togglePropertyList: boolean;
}

export interface SourceTarget {
  propertyName: string;
  selectedModel: string;
}

export interface FormDataObj {
  [key: string]: any;
}

export interface FormDataStackItem {
  source: SourceTarget;
  target: SourceTarget;
  formData: FormDataObj;
  key: string;
}
