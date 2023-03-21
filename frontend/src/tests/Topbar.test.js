import '@testing-library/jest-dom/extend-expect'
import { render, screen } from '@testing-library/react';
import Topbar from '../scenes/global/Topbar';

test('renders Topbar correctly', () => {
    render(
        <Topbar />
    );

    // // check search box
    // const searchBox = screen.getByRole("textbox");
    // expect(searchBox).toBeInTheDocument();

    // // check Place Holder
    // const placeholder = screen.getByPlaceholderText("Enter Region");
    // expect(placeholder).toBeInTheDocument();

    // check Light Mode Outlined Icon
    const LightModeOutlinedIcon = screen.getByTestId("LightModeOutlinedIcon");
    expect(LightModeOutlinedIcon).toBeInTheDocument();

    // const element = screen.getByText("element");
    // expect(element).toBeInTheDocument();

    // // check Search Icon
    // const SearchIcon = screen.getByTestId("SearchIcon");
    // expect(SearchIcon).toBeInTheDocument();
    
});
