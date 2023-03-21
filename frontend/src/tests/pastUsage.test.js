import { render } from 'react-dom';
import { screen } from "@testing-library/react"
import pastUsage from '../scenes/pastUsage/index';

window.ResizeObserver = jest.fn(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

describe('Home component', () => {
  it('should render without errors', () => {
    const div = document.createElement('div');
    render(<pastUsage />, div);
  });
});
