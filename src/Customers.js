```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => {
        setCustomers(data);
        setLoading(false);
      });
  }, []);

  const removeCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  const renderLoading = () => <div>Loading customers...</div>;

  const renderCustomers = () => (
    <ul>
      {customers.map(customer => (
        <li key={customer.id}>
          {customer.name}
          <button onClick={() => removeCustomer(customer.id)}>Remove</button>
        </li>
      ))}
    </ul>
  );

  return (
    <div>
      <h1>Customer List</h1>
      {loading ? renderLoading() : renderCustomers()}
    </div>
  );
};

export default CustomerList;
```