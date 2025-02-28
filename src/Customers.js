```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchData();
  }, []);

  const handleAddCustomer = () => {
    if (newCustomer.name && newCustomer.email) {
      setCustomers([...customers, newCustomer]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  const handleDeleteCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Search customers" 
        value={searchTerm} 
        onChange={(e) => setSearchTerm(e.target.value)} 
      />
      <h2>Add New Customer</h2>
      <input 
        type="text" 
        placeholder="Name" 
        value={newCustomer.name} 
        onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={newCustomer.email} 
        onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })} 
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <h2>Customer List</h2>
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} ({customer.email}) 
            <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```