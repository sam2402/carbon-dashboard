// import '@testing-library/jest-dom/extend-expect'
// import { render, screen } from '@testing-library/react';
// import Index from '../scenes/home/index';
// import { BrowserRouter } from "react-router-dom";


// test('renders dashboard title and subtitle', () => {
//   // render(<Index />);

//   render(
//     <BrowserRouter>
//       <Index />
//     </BrowserRouter>
//   );


//   const title = screen.getByText('DASHBOARD');
//   const subtitle = screen.getByText('Welcome to your dashboard');
//   expect(title).toBeInTheDocument();
//   expect(subtitle).toBeInTheDocument();
// });








// import { act, render, waitFor } from '@testing-library/react';
// import { BrowserRouter } from 'react-router-dom';
// import Home from '../scenes/home/index';

// describe('Home component', () => {
//   it('should render the header with title and subtitle', async () => {
//     await act(async () => {
//       render(
//         <BrowserRouter>
//           <Home />
//         </BrowserRouter>
//       );
//     });

//     await waitFor(() => {
//       expect(screen.getByText('DASHBOARD')).toBeInTheDocument();
//       expect(screen.getByText('Welcome to your dashboard')).toBeInTheDocument();
//     });
//   });

//   it('should render the geography chart', async () => {
//     await act(async () => {
//       render(
//         <BrowserRouter>
//           <Home />
//         </BrowserRouter>
//       );
//     });

//     await waitFor(() => {
//       expect(screen.getByRole('region')).toBeInTheDocument();
//     });
//   });

//   it('should match snapshot', async () => {
//     let container;
//     await act(async () => {
//       container = render(
//         <BrowserRouter>
//           <Home />
//         </BrowserRouter>
//       ).container;
//     });
//     expect(container).toMatchSnapshot();
//   });
// });










import { render } from 'react-dom';
import { screen } from "@testing-library/react"
import Home from '../scenes/home/index';

window.ResizeObserver = jest.fn(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

describe('Home component', () => {
  it('should render without errors', () => {
    const div = document.createElement('div');
    render(<Home />, div);
  });

  // const title = screen.getByText('DASHBOARD');
  // const subtitle = screen.getByText('Welcome to your dashboard');
  // expect(title).toBeInTheDocument();
  // expect(subtitle).toBeInTheDocument();

});
