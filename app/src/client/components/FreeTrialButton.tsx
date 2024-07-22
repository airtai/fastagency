// import { useAuth } from 'wasp/client/auth';
// import { stripePayment } from 'wasp/client/operations';

// import { useState } from 'react';
// import { useHistory } from 'react-router-dom';
// import { TierIds } from '../../shared/constants';
// import Button from './Button';

// interface FreeTrialButtonProps {
//   theme?: 'light' | 'dark';
// }

// export default function FreeTrialButton({ theme = 'dark' }: FreeTrialButtonProps) {
//   const history = useHistory();
//   const [isLoading, setIsLoading] = useState<boolean>(false);
//   const { data: user } = useAuth();

//   async function handleClick(tierId: string) {
//     if (!user) {
//       history.push('/login');
//     } else {
//       try {
//         // setIsStripePaymentLoading(tierId);
//         setIsLoading(true);
//         let stripeResults = await stripePayment(tierId);

//         if (stripeResults?.sessionUrl) {
//           window.open(stripeResults.sessionUrl, '_self');
//         }
//       } catch (error: any) {
//         console.error(error?.message ?? 'Something went wrong.');
//       } finally {
//         // setIsStripePaymentLoading(false);
//         setIsLoading(false);
//       }
//     }
//   }

//   return (
//     <Button
//       onClick={(e) => {
//         e.preventDefault();
//         handleClick(TierIds.PRO);
//       }}
//       label={!isLoading ? 'Free Trial' : 'Loading...'}
//       theme={theme}
//     />
//   );
// }
