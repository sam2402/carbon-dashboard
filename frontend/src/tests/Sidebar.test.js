import "@testing-library/jest-dom";
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from "react-router-dom";
import Sidebar from '../scenes/global/Sidebar';

describe("Sidebar", () => {
  test("renders the dashboard link", () => {
    const { getByText } = render(
      <BrowserRouter>
        <Sidebar />
      </BrowserRouter>
    );
    const titleElement = getByText(/Carbon Analysis Dashboard/i);
    expect(titleElement).toBeInTheDocument();

    const homeElement = getByText(/Home/i);
    expect(homeElement).toBeInTheDocument();

    const dataElement = getByText(/Data/i);
    expect(dataElement).toBeInTheDocument();

    const pastElement = getByText(/Past Usage/i);
    expect(pastElement).toBeInTheDocument();

    const futureElement = getByText(/Future Prediction/i);
    expect(futureElement).toBeInTheDocument();

    const futureAdviceElement = getByText(/Future Advice/i);
    expect(futureAdviceElement).toBeInTheDocument();

    const resourceGroupElement = getByText(/Resource Group/i);
    expect(resourceGroupElement).toBeInTheDocument();

    const regionElement = getByText(/Region/i);
    expect(regionElement).toBeInTheDocument();
  });
});
