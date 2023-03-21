import '@testing-library/jest-dom/extend-expect'
import { render, screen } from '@testing-library/react';
import Region from '../scenes/region/index';

describe('Region component', () => {
  test('renders all accordion sections with correct titles', () => {
    render(<Region />);
    const accordionTitles = [
      'Energy Type',
      'Resources Configuration',
      'Location',
      'Cooling Type',
    ];
    accordionTitles.forEach((title) => {
      const titleElement = screen.getByText(title);
      expect(titleElement).toBeInTheDocument();
    });
  });
});
