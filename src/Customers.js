```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleAddCustomer = () => {
    if (newCustomer) {
      setCustomers([...customers, { id: customers.length + 1, name: newCustomer }]);
      setNewCustomer("");
    }
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        placeholder="Search customers..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
      <input
        type="text"
        placeholder="Add new customer"
        value={newCustomer}
        onChange={(e) => setNewCustomer(e.target.value)}
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```