import { JsonSchema } from '../interfaces/BuildPageInterfaces';

export function flattenSchema(schema: JsonSchema): JsonSchema {
  return schema;
  //   if (!schema.$defs) {
  //     return schema;
  //   }

  //   //   const flattenedSchema = { ...schema };
  //   //   delete flattenedSchema.$defs;

  //   //   for (const key in flattenedSchema.properties) {
  //   //     if (flattenedSchema.properties[key].allOf) {
  //   //       flattenedSchema.properties[key].allOf?.map((item: any) => {
  //   //         if (item.$ref) {
  //   //           const refKey = item.$ref.split('/').pop();
  //   //           return { [refKey as string]: schema.$defs![refKey as string] };
  //   //         }
  //   //         return item;
  //   //       });
  //   //     }
  //   //   }

  //   return flattenedSchema;
}
