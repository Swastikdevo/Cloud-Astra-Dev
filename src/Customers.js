```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = ({ customers, onRemoveCustomer }) => {
  const [filteredCustomers, setFilteredCustomers] = useState(customers);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    setFilteredCustomers(
      customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm, customers]);

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} 
            <button onClick={() => onRemoveCustomer(customer.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```