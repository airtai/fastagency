import React, { useState } from 'react';
import {
  Card,
  CardBody,
  Stack,
  Heading,
  Text,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Image,
  Box,
  ChakraProvider,
} from '@chakra-ui/react';

export default function TutorialPage() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedVideo, setSelectedVideo] = useState('');

  const data = [
    {
      link: 'https://www.youtube.com/embed/9y4cDOkWIBw',
      heading: 'Building and Deploying SaaS with AI Agents and Multi-Agent Teams',
      description:
        'Build a powerful SaaS solution with FastAgency. This tutorial demonstrates how to incorporate AI agents and multi-agent teams into your app effortlessly.',
      thumbnail: `https://img.youtube.com/vi/9y4cDOkWIBw/0.jpg`,
    },
    {
      link: 'https://www.youtube.com/embed/mD105mzcbP8',
      heading: 'Creating and Integrating a Web Surfer Agent',
      description:
        'Enhance your SaaS with web surfing capabilities using FastAgency. See how to build and deploy an app that utilizes this powerful agent.',
      thumbnail: `https://img.youtube.com/vi/mD105mzcbP8/0.jpg`,
    },
  ];

  const handleCardClick = (videoLink: string) => {
    setSelectedVideo(videoLink);
    onOpen();
  };

  return (
    <ChakraProvider>
      <div className='mx-auto max-w-7xl pl-10 pr-10 text-airt-font-base pt-10 pb-24 sm:pb-32 lg:gap-x-8 lg:py-5 lg:px-8'>
        <h1 className='text-title-md2 font-semibold text-airt-primary dark:text-white my-4'>Tutorials</h1>
        <div className='rounded-lg border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark min-h-[300px] sm:min-h-[600px]'>
          <div className='p-10'>
            <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
              {data.map((item, index) => (
                <div
                  key={index}
                  className='video-responsive bg-airt-primary p-2 rounded-lg hover:opacity-90 hover:cursor-pointer transition-all duration-300 hover:-translate-y-1'
                  onClick={() => handleCardClick(item.link)}
                >
                  <Card backgroundColor='airt-primary'>
                    <CardBody>
                      <Image src={item.thumbnail} alt={item.heading} />
                      <Stack className='mt-3 text-airt-font-base'>
                        <Heading fontSize='md'>{item.heading}</Heading>
                        <Text fontSize='sm'>{item.description}</Text>
                      </Stack>
                    </CardBody>
                  </Card>
                </div>
              ))}
            </div>
          </div>

          <Modal isOpen={isOpen} onClose={onClose} size='full' isCentered>
            <ModalOverlay bg='blackAlpha.300' backdropFilter='blur(5px)' />
            <ModalContent bg='transparent' boxShadow='none'>
              <ModalCloseButton color='white' />
              <ModalBody display='flex' alignItems='center' justifyContent='center'>
                <Box
                  width='100%'
                  maxWidth='800px'
                  height='450px'
                  position='relative'
                  overflow='hidden'
                  borderRadius='md'
                >
                  <iframe
                    src={`${selectedVideo}?autoplay=1`}
                    title='YouTube video player'
                    width='100%'
                    height='100%'
                    allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
                    allowFullScreen
                    style={{ position: 'absolute', top: 0, left: 0 }}
                  />
                </Box>
              </ModalBody>
            </ModalContent>
          </Modal>
        </div>
      </div>
    </ChakraProvider>
  );
}
