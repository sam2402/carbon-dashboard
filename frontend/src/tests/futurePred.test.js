import { render } from 'react-dom';
import { screen } from "@testing-library/react"
import futurePred from '../scenes/futurePred/index';

window.ResizeObserver =
    window.ResizeObserver ||
    jest.fn().mockImplementation(() => ({
        disconnect: jest.fn(),
        observe: jest.fn(),
        unobserve: jest.fn(),
    }));

describe('Home component', () => {
  it('should render without errors', () => {
    const div = document.createElement('div');
    render(<futurePred />, div);
  });
});

// import { render, screen, fireEvent } from '@testing-library/react';
// import FuturePred from '../scenes/futurePred/index';
// // import { ResizeObserver } from 'react-resize-observer';
// import ResizeObserver from 'resize-observer-polyfill';
// import { act } from 'react-dom/test-utils';


// describe('FuturePred', () => {
//   it('should render the Resource Group select', () => {
//     act(() => {
//       const { container } = render(
//         <ResizeObserver
//           onResize={(react) => {
//             container.style.width = `500px`;
//           }}
//         >
//           <FuturePred />
//         </ResizeObserver>
//       );
//     });
    
//     const resourceGroupSelect = screen.getByLabelText('Resource Group');
//     expect(resourceGroupSelect).toBeInTheDocument();
//   });


// });
