```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    fetch('/api/customers')
      .then(response => response.json())
      .then(data => setCustomers(data));
  }, []);

  const removeCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name}
            <button onClick={() => removeCustomer(customer.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```