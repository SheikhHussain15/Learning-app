import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

describe('Basic Component Rendering', () => {
  it('renders a simple div', () => {
    render(<div data-testid="test-div">Hello World</div>);
    expect(screen.getByTestId('test-div')).toHaveTextContent('Hello World');
  });

  it('renders a button', () => {
    render(<button>Click me</button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });
});
