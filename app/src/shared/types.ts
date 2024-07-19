export type StripePaymentResult = {
  sessionUrl: string | null;
  sessionId: string;
};

export type Subtask = {
  description: string; // detailed breakdown and description of sub-task
  time: number; // total time it takes to complete given main task in hours, e.g. 2.75
  mainTaskName: string; // name of main task related to subtask
};

export type MainTask = {
  name: string;
  priority: 'low' | 'medium' | 'high';
};
