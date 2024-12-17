```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([{ id: 1, name: 'John Doe', email: 'john@example.com' }]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [editId, setEditId] = useState(null);

  const addCustomer = () => {
    if (name && email) {
      setCustomers([...customers, { id: Date.now(), name, email }]);
      setName('');
      setEmail('');
    }
  };

  const deleteCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  const editCustomer = (customer) => {
    setName(customer.name);
    setEmail(customer.email);
    setEditId(customer.id);
  };

  const updateCustomer = () => {
    setCustomers(customers.map(customer => customer.id === editId ? { ...customer, name, email } : customer));
    setName('');
    setEmail('');
    setEditId(null);
  };

  return (
    <div>
      <h1>Customer Management System</h1>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <button onClick={editId ? updateCustomer : addCustomer}>{editId ? 'Update' : 'Add'} Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => editCustomer(customer)}>Edit</button>
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```