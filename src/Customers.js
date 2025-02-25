```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddCustomer({ name, email, phone });
    setName('');
    setEmail('');
    setPhone('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input type="text" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} required />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const addCustomer = (customer) => {
    setCustomers((prev) => [...prev, customer]);
  };

  const filteredCustomers = customers.filter((customer) => customer.name.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <div>
      <CustomerForm onAddCustomer={addCustomer} />
      <input type="text" placeholder="Search..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email} - {customer.phone}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```