```javascript
import React, { useState, useEffect } from 'react';

const CustomerTable = ({ customers }) => {
  const [filter, setFilter] = useState('');
  const [sortedCustomers, setSortedCustomers] = useState([]);

  useEffect(() => {
    setSortedCustomers(customers.sort((a, b) => a.name.localeCompare(b.name)));
  }, [customers]);

  const filteredCustomers = sortedCustomers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Search by name"
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
          </tr>
        </thead>
        <tbody>
          {filteredCustomers.map(customer => (
            <tr key={customer.id}>
              <td>{customer.name}</td>
              <td>{customer.email}</td>
              <td>{customer.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerTable;
```