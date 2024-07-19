import React, { useEffect, useRef, useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import Logo from '../static/logo.svg';
import { cn } from '../../shared/utils';

interface NavLinkItem {
  label: string;
  svgIcon: React.ReactNode;
  componentName: string;
}

export const navLinkItems: NavLinkItem[] = [
  {
    label: 'Secrets',
    svgIcon: (
      <svg
        className='fill-current stroke-current -mt-1'
        width='18'
        height='18'
        viewBox='0 0 34 34'
        xmlns='http://www.w3.org/2000/svg'
      >
        <title>key</title>
        <path
          d='M27.339 8.365l0.63-1.011 1.513 0.942 1.065-1.555-2.683-1.838c-1.513 2.208-3.368 1.191-5.172-0.028l1.654-2.413-2.101-1.44-11.242 16.406-1.431-0.999c-1.527-1.065-3.411 1.592-1.864 2.671l1.454 1.015-0.21 0.307c-2.85-1.433-5.949-1.161-7.289 0.796h0c-1.518 2.215-0.209 5.752 2.903 7.885s6.858 2.059 8.376-0.156c1.345-1.962 0.49-4.949-1.886-7.088l0.196-0.286 1.238 0.864c1.42 0.991 3.319-1.656 1.864-2.671l-1.261-0.88 6.545-9.552c1.731 1.195 3.456 2.533 2.091 4.525l2.683 1.838 1.802-2.63-1.678-1.045 0.689-1.106 1.727 1.075 1.121-1.635-2.353-1.465 0.689-1.106 0.933 0.581zM6.183 28.027c-1.135 0-2.055-0.92-2.055-2.055s0.92-2.055 2.055-2.055 2.055 0.92 2.055 2.055c-0 1.135-0.92 2.055-2.055 2.055z'
          fill='none'
          stroke='currentColor'
          strokeMiterlimit='10'
          strokeWidth='1'
        ></path>
      </svg>
    ),
    componentName: 'secret',
  },
  {
    label: 'LLMs',
    svgIcon: (
      <svg
        fill='currentColor'
        stroke='currentColor'
        strokeWidth='0.5'
        version='1.1'
        id='Layer_1'
        xmlns='http://www.w3.org/2000/svg'
        xmlnsXlink='http://www.w3.org/1999/xlink'
        viewBox='0 0 32 32'
        width='18'
        height='18'
        xmlSpace='preserve'
        className='-mt-1'
      >
        <path d='M12,30.36c-1.47,0-2.852-0.766-3.653-2.011C5.703,28.24,3.64,26.106,3.64,23.5 c0-0.899,0.252-1.771,0.733-2.544C2.678,19.887,1.64,18.021,1.64,16s1.038-3.886,2.733-4.957C3.893,10.271,3.64,9.4,3.64,8.5 c0-2.63,2.101-4.779,4.712-4.858C9.155,2.402,10.534,1.64,12,1.64c2.404,0,4.36,1.956,4.36,4.36v4.64H25 c0.904,0,1.64-0.736,1.64-1.64V7.312c-0.575-0.158-1-0.686-1-1.312c0-0.75,0.61-1.36,1.36-1.36S28.36,5.25,28.36,6 c0,0.625-0.425,1.153-1,1.312V9c0,1.301-1.059,2.36-2.36,2.36h-8.64v2.28h11.329c0.158-0.576,0.687-1,1.312-1 c0.75,0,1.36,0.61,1.36,1.36s-0.61,1.36-1.36,1.36c-0.625,0-1.153-0.424-1.312-1H16.36v3.28h11.329c0.158-0.575,0.687-1,1.312-1 c0.75,0,1.36,0.61,1.36,1.36s-0.61,1.36-1.36,1.36c-0.625,0-1.153-0.425-1.312-1H16.36v2.279H25c1.302,0,2.36,1.059,2.36,2.36v1.688 c0.575,0.158,1,0.687,1,1.312c0,0.75-0.61,1.36-1.36,1.36s-1.36-0.61-1.36-1.36c0-0.625,0.425-1.153,1-1.312V23 c0-0.904-0.735-1.64-1.64-1.64h-8.64V26C16.36,28.404,14.404,30.36,12,30.36z M8.721,27.628l0.143,0.186 C9.526,28.957,10.699,29.64,12,29.64c2.007,0,3.64-1.633,3.64-3.64V6c0-2.007-1.633-3.64-3.64-3.64 c-1.301,0-2.474,0.683-3.137,1.826L8.747,4.365C8.493,4.869,8.36,5.431,8.36,6c0,0.64,0.168,1.269,0.487,1.82L8.224,8.18 C7.842,7.521,7.64,6.766,7.64,6c0-0.547,0.103-1.088,0.3-1.593C5.901,4.694,4.36,6.42,4.36,8.5c0,0.876,0.283,1.722,0.817,2.446 l0.246,0.333l-0.364,0.197C3.394,12.377,2.36,14.11,2.36,16c0,1.785,0.922,3.43,2.427,4.365C5.713,19.268,7.061,18.64,8.5,18.64 v0.721c-1.206,0-2.336,0.517-3.125,1.424l-0.198,0.27C4.643,21.778,4.36,22.624,4.36,23.5c0,2.283,1.857,4.14,4.14,4.14 L8.721,27.628z M27,25.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S27.353,25.36,27,25.36z M29,17.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S29.353,17.36,29,17.36z M29,13.36 c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64S29.353,13.36,29,13.36z M27,5.36 c-0.353,0-0.64,0.287-0.64,0.64S26.647,6.64,27,6.64S27.64,6.353,27.64,6S27.353,5.36,27,5.36z M12,28.36v-0.72 c0.904,0,1.64-0.735,1.64-1.64h0.72C14.36,27.302,13.301,28.36,12,28.36z M9,26.36c-1.577,0-2.86-1.283-2.86-2.86h0.72 c0,1.18,0.96,2.14,2.14,2.14C9,25.64,9,26.36,9,26.36z M12,24.36c-1.301,0-2.36-1.059-2.36-2.36s1.059-2.36,2.36-2.36v0.721 c-0.904,0-1.64,0.735-1.64,1.64s0.736,1.64,1.64,1.64V24.36z M6.332,16.667C5.886,16.221,5.64,15.629,5.64,15 c0-1.39,0.97-2.36,2.36-2.36c0.641,0,1.218,0.238,1.669,0.689l-0.51,0.509C8.847,13.525,8.446,13.36,8,13.36 c-0.996,0-1.64,0.644-1.64,1.64c0,0.437,0.171,0.848,0.48,1.158L6.332,16.667z M12,12.86v-0.72c0.904,0,1.64-0.736,1.64-1.64 S12.904,8.86,12,8.86V8.14c1.301,0,2.36,1.059,2.36,2.36S13.301,12.86,12,12.86z M14.36,6h-0.72c0-0.904-0.736-1.64-1.64-1.64 S10.36,5.096,10.36,6H9.64c0-1.301,1.059-2.36,2.36-2.36S14.36,4.699,14.36,6z' />
      </svg>
    ),
    componentName: 'llm',
  },
  {
    label: 'ToolBoxes',
    svgIcon: (
      <svg className='fill-current -mt-1' width='18' height='18' viewBox='0 0 18 18' xmlns='http://www.w3.org/2000/svg'>
        <g transform='scale(0.03515625)'>
          <g>
            <g>
              <path
                d='M500.23,270.051h-74.54V212.66c0-6.501-5.271-11.77-11.77-11.77h-48.1l27.688-47.958l64.046,36.977
            c1.804,1.043,3.837,1.577,5.885,1.577c1.019,0,2.044-0.133,3.046-0.401c3.017-0.809,5.586-2.78,7.147-5.484l20.598-35.678
            c2.533-4.388,1.975-9.906-1.389-13.696C445.913,83.333,394.793,29.371,331.424,1.649c-5.491-2.402-11.913-0.294-14.91,4.899
            l-38.253,66.256c-3.251,5.63-1.322,12.828,4.308,16.078l39.586,22.855l-69.394,120.189l-78.893-116.953l-2.194-16.818
            c-0.237-1.813-0.892-3.544-1.914-5.059l-29.837-44.232c-3.636-5.39-10.952-6.81-16.339-3.176l-53.66,36.193
            c-2.588,1.746-4.377,4.448-4.973,7.512c-0.596,3.064,0.051,6.24,1.796,8.828l29.837,44.232c1.02,1.513,2.379,2.767,3.968,3.665
            l14.769,8.345l77.97,115.587H147.67l-46.458-95.485c-2.845-5.845-9.89-8.277-15.733-5.434c-5.845,2.845-8.278,9.888-5.434,15.733
            l41.447,85.186H91.712l-18.556-42.205c-2.618-5.951-9.566-8.653-15.512-6.037c-5.951,2.616-8.655,9.561-6.038,15.512
            l14.39,32.732H11.77c-6.5,0-11.77,5.269-11.77,11.77v64.736c0,6.501,5.271,11.77,11.77,11.77h20.598v141.241
            c0,6.501,5.271,11.77,11.77,11.77h423.724c6.499,0,11.77-5.269,11.77-11.77V358.328h20.598c6.5,0,11.77-5.269,11.77-11.77
            v-64.736C512,275.32,506.729,270.051,500.23,270.051z M402.15,224.43v45.621h-76.259l26.338-45.621H402.15z M304.533,74.381
            l26.982-46.734c52.385,25.827,96.917,71.78,138.08,117.868l-10.464,18.122L304.533,74.381z M263.734,260.013
            c0.005-0.008,0.007-0.016,0.012-0.025l78.799-136.482l30.578,17.654l-74.412,128.89h-40.774L263.734,260.013z M133.285,139
            c-1.02-1.512-2.379-2.767-3.968-3.665l-14.769-8.345L92.846,94.815l34.144-23.029l21.702,32.171l2.194,16.818
            c0.237,1.813,0.892,3.544,1.914,5.059l86.868,128.772l-8.917,15.444h-9.063L133.285,139z M456.092,438.952h-48.846
            c-6.499,0-11.77,5.269-11.77,11.77s5.271,11.77,11.77,11.77h48.846v25.306H55.908v-25.306h48.846
            c6.499,0,11.77-5.269,11.77-11.77s-5.271-11.77-11.77-11.77H55.908v-80.625h135.356v41.195c0,6.501,5.271,11.77,11.77,11.77
            h105.931c6.499,0,11.77-5.269,11.77-11.77v-41.195h135.356V438.952z M214.805,387.752v-29.425h82.391v29.425H214.805z
             M488.46,334.787H23.54v-41.195h464.92V334.787z'
              />
              <path
                d='M149.677,438.952H148.5c-6.499,0-11.77,5.269-11.77,11.77s5.271,11.77,11.77,11.77h1.177
            c6.499,0,11.77-5.269,11.77-11.77S156.176,438.952,149.677,438.952z'
              />
              <path
                d='M362.323,462.492h1.177c6.499,0,11.77-5.269,11.77-11.77s-5.271-11.77-11.77-11.77h-1.177
            c-6.499,0-11.77,5.269-11.77,11.77S355.824,462.492,362.323,462.492z'
              />
            </g>
          </g>
        </g>
      </svg>
    ),
    componentName: 'toolbox',
  },
  {
    label: 'Agents',
    svgIcon: (
      <svg
        fill='currentColor'
        stroke='currentColor'
        strokeWidth='0.5' // Adding a small stroke width to make the border visible, adjust as needed
        version='1.1'
        id='Layer_1'
        xmlns='http://www.w3.org/2000/svg'
        xmlnsXlink='http://www.w3.org/1999/xlink'
        viewBox='0 0 32 32'
        xmlSpace='preserve'
        width='18'
        height='18'
        className='-mt-1'
      >
        <path
          id='machine--learning--04_1_'
          d='M23,30.36H9c-2.404,0-4.36-1.956-4.36-4.36V15c0-2.404,1.956-4.36,4.36-4.36h3.659
    c0.167-1.566,1.415-2.813,2.981-2.981V5.333c-1.131-0.174-2-1.154-2-2.333c0-1.301,1.059-2.36,2.36-2.36
    c1.302,0,2.36,1.059,2.36,2.36c0,1.179-0.869,2.159-2,2.333V7.66c1.566,0.167,2.814,1.415,2.981,2.981H23
    c2.404,0,4.36,1.956,4.36,4.36v11C27.36,28.404,25.404,30.36,23,30.36z M9,11.36c-2.007,0-3.64,1.633-3.64,3.64v11
    c0,2.007,1.633,3.64,3.64,3.64h14c2.007,0,3.64-1.633,3.64-3.64V15c0-2.007-1.633-3.64-3.64-3.64H9z M13.384,10.64h5.231
    C18.439,9.354,17.334,8.36,16,8.36C14.667,8.36,13.561,9.354,13.384,10.64z M16,1.36c-0.904,0-1.64,0.736-1.64,1.64
    S15.096,4.64,16,4.64c0.904,0,1.64-0.736,1.64-1.64S16.904,1.36,16,1.36z M20,27.36h-8c-1.301,0-2.36-1.059-2.36-2.36
    s1.059-2.36,2.36-2.36h8c1.302,0,2.36,1.059,2.36,2.36S21.302,27.36,20,27.36z M12,23.36c-0.904,0-1.64,0.735-1.64,1.64
    s0.736,1.64,1.64,1.64h8c0.904,0,1.64-0.735,1.64-1.64s-0.735-1.64-1.64-1.64H12z M31,23.86h-2c-0.199,0-0.36-0.161-0.36-0.36V15
    c0-0.199,0.161-0.36,0.36-0.36h2c0.199,0,0.36,0.161,0.36,0.36v8.5C31.36,23.699,31.199,23.86,31,23.86z M29.36,23.14h1.279v-7.78
    H29.36V23.14z M3,23.86H1c-0.199,0-0.36-0.161-0.36-0.36V15c0-0.199,0.161-0.36,0.36-0.36h2c0.199,0,0.36,0.161,0.36,0.36v8.5
    C3.36,23.699,3.199,23.86,3,23.86z M1.36,23.14h1.28v-7.78H1.36V23.14z M20,20.36c-1.302,0-2.36-1.059-2.36-2.36
    s1.059-2.36,2.36-2.36s2.36,1.059,2.36,2.36C22.36,19.302,21.302,20.36,20,20.36z M20,16.36c-0.904,0-1.64,0.736-1.64,1.64
    s0.735,1.64,1.64,1.64s1.64-0.735,1.64-1.64S20.904,16.36,20,16.36z M12,20.36c-1.301,0-2.36-1.059-2.36-2.36s1.059-2.36,2.36-2.36
    s2.36,1.059,2.36,2.36C14.36,19.302,13.301,20.36,12,20.36z M12,16.36c-0.904,0-1.64,0.736-1.64,1.64s0.736,1.64,1.64,1.64
    s1.64-0.735,1.64-1.64S12.904,16.36,12,16.36z'
        />
      </svg>
    ),
    componentName: 'agent',
  },
  {
    label: 'Teams',
    svgIcon: (
      <svg
        width='18px'
        height='18px'
        viewBox='0 0 24 24'
        id='team'
        xmlns='http://www.w3.org/2000/svg'
        className='custom-svg'
      >
        <g id='_24x24_user--dark' data-name='24x24/user--dark'>
          <rect id='Rectangle' width='24' height='24' fill='none' />
        </g>
        <path
          id='Combined_Shape'
          data-name='Combined Shape'
          d='M0,12.106C0,8.323,4.5,9.08,4.5,7.567a2.237,2.237,0,0,0-.41-1.513A3.5,3.5,0,0,1,3,3.4,3.222,3.222,0,0,1,6,0,3.222,3.222,0,0,1,9,3.4,3.44,3.44,0,0,1,7.895,6.053,2.333,2.333,0,0,0,7.5,7.567c0,1.513,4.5.757,4.5,4.54,0,0-1.195.894-6,.894S0,12.106,0,12.106Z'
          transform='translate(6 8)'
          fill='none'
          stroke='currentColor'
          strokeMiterlimit='10'
          strokeWidth='1.5'
        />
        <path
          id='Combined_Shape-2'
          data-name='Combined Shape'
          d='M4.486,12.967c-.569-.026-1.071-.065-1.512-.114A6.835,6.835,0,0,1,0,12.106C0,8.323,4.5,9.08,4.5,7.567a2.237,2.237,0,0,0-.41-1.513A3.5,3.5,0,0,1,3,3.4,3.222,3.222,0,0,1,6,0,3.222,3.222,0,0,1,9,3.4'
          transform='translate(1 3)'
          fill='none'
          stroke='currentColor'
          strokeMiterlimit='10'
          strokeWidth='1.5'
        />
        <path
          id='Combined_Shape-3'
          data-name='Combined Shape'
          d='M-4.486,12.967c.569-.026,1.071-.065,1.512-.114A6.835,6.835,0,0,0,0,12.106C0,8.323-4.5,9.08-4.5,7.567a2.237,2.237,0,0,1,.41-1.513A3.5,3.5,0,0,0-3,3.4,3.222,3.222,0,0,0-6,0,3.222,3.222,0,0,0-9,3.4'
          transform='translate(23 3)'
          fill='none'
          stroke='currentColor'
          strokeMiterlimit='10'
          strokeWidth='1.5'
        />
      </svg>
    ),
    componentName: 'team',
  },
  {
    label: 'Deployments',
    svgIcon: (
      <svg
        width='26px'
        height='26px'
        viewBox='0 0 24 24'
        id='team'
        xmlns='http://www.w3.org/2000/svg'
        className='custom-svg'
      >
        <style>{`.st0{fill:none;stroke:currentColor;stroke-width:1;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:10;}`}</style>
        <rect x='1' y='3' className='st0' width='16' height='14' />
        <line className='st0' x1='7' y1='5' x2='7' y2='5' />
        <line className='st0' x1='5' y1='5' x2='5' y2='5' />
        <line className='st0' x1='3' y1='5' x2='3' y2='5' />
        <line className='st0' x1='1' y1='6' x2='17' y2='6' />
      </svg>
    ),
    componentName: 'deployment',
  },
];

interface SidebarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (arg: boolean) => void;
  onSideNavItemClick: (selectedItem: string) => void;
  sideNavSelectedItem: string;
}

const CustomSidebar = ({ sidebarOpen, setSidebarOpen, onSideNavItemClick, sideNavSelectedItem }: SidebarProps) => {
  const location = useLocation();
  const { pathname } = location;

  const trigger = useRef<any>(null);
  const sidebar = useRef<any>(null);

  const storedSidebarExpanded = localStorage.getItem('sidebar-expanded');
  const [sidebarExpanded, setSidebarExpanded] = useState(
    storedSidebarExpanded === null ? false : storedSidebarExpanded === 'true'
  );

  // close on click outside
  useEffect(() => {
    const clickHandler = ({ target }: MouseEvent) => {
      if (!sidebar.current || !trigger.current) return;
      if (!sidebarOpen || sidebar.current.contains(target) || trigger.current.contains(target)) return;
      setSidebarOpen(false);
    };
    document.addEventListener('click', clickHandler);
    return () => document.removeEventListener('click', clickHandler);
  });

  // close if the esc key is pressed
  useEffect(() => {
    const keyHandler = ({ keyCode }: KeyboardEvent) => {
      if (!sidebarOpen || keyCode !== 27) return;
      setSidebarOpen(false);
    };
    document.addEventListener('keydown', keyHandler);
    return () => document.removeEventListener('keydown', keyHandler);
  });

  useEffect(() => {
    localStorage.setItem('sidebar-expanded', sidebarExpanded.toString());
    if (sidebarExpanded) {
      document.querySelector('body')?.classList.add('sidebar-expanded');
    } else {
      document.querySelector('body')?.classList.remove('sidebar-expanded');
    }
  }, [sidebarExpanded]);

  const handleClick = (selectedItemLable: string) => {
    onSideNavItemClick(selectedItemLable);
    setSidebarOpen(false);
  };

  return (
    <aside
      ref={sidebar}
      style={{ top: '80px' }}
      className={cn(
        'h-[calc(100vh-80px)] absolute left-0 z-9999 flex w-75 flex-col overflow-y-hidden bg-airt-primary duration-300 ease-linear dark:bg-boxdark lg:static lg:translate-x-0',
        {
          'translate-x-0': sidebarOpen,
          '-translate-x-full': !sidebarOpen,
        }
      )}
    >
      {/* <!-- SIDEBAR HEADER --> */}
      <div className='flex justify-end gap-2 px-6 py-5.5 lg:py-6.5'>
        {/* <NavLink to='/'>
          <img src={Logo} alt='Logo' width={50} />
        </NavLink> */}

        <button
          ref={trigger}
          onClick={() => setSidebarOpen(!sidebarOpen)}
          aria-controls='sidebar'
          aria-expanded={sidebarOpen}
          className='block lg:hidden text-airt-font-base'
        >
          <svg width='24px' height='24px' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'>
            <path
              d='M20.7457 3.32851C20.3552 2.93798 19.722 2.93798 19.3315 3.32851L12.0371 10.6229L4.74275 3.32851C4.35223 2.93798 3.71906 2.93798 3.32854 3.32851C2.93801 3.71903 2.93801 4.3522 3.32854 4.74272L10.6229 12.0371L3.32856 19.3314C2.93803 19.722 2.93803 20.3551 3.32856 20.7457C3.71908 21.1362 4.35225 21.1362 4.74277 20.7457L12.0371 13.4513L19.3315 20.7457C19.722 21.1362 20.3552 21.1362 20.7457 20.7457C21.1362 20.3551 21.1362 19.722 20.7457 19.3315L13.4513 12.0371L20.7457 4.74272C21.1362 4.3522 21.1362 3.71903 20.7457 3.32851Z'
              fill='rgb(138 153 175)'
            />
          </svg>
        </button>
      </div>
      {/* <!-- SIDEBAR HEADER --> */}

      <div className='no-scrollbar flex flex-col overflow-y-auto duration-300 ease-linear'>
        {/* <!-- Sidebar Menu --> */}
        <nav className='px-4 lg:mt-9 lg:px-6'>
          {/* <!-- Menu Group --> */}
          <div>
            <h3 className='mb-4 ml-4 text-sm font-semibold text-bodydark2'>MENU</h3>

            <ul className='mb-6 flex flex-col gap-1.5'>
              {navLinkItems.map((item) => (
                <li key={item.label}>
                  <NavLink
                    to=''
                    onClick={(e) => {
                      e.preventDefault();
                      handleClick(item.componentName);
                    }}
                    className={cn(
                      'group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-airt-font-base duration-300 ease-in-out hover:bg-airt-secondary hover:text-airt-primary dark:hover:bg-meta-4',
                      {
                        'bg-airt-secondary text-airt-primary': item.componentName === sideNavSelectedItem,
                      }
                    )}
                  >
                    {item.svgIcon}
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        </nav>
        {/* <!-- Sidebar Menu --> */}
      </div>
    </aside>
  );
};

export default CustomSidebar;
