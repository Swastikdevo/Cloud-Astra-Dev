```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [editingIndex, setEditingIndex] = useState(-1);

  const addOrUpdateCustomer = () => {
    if (editingIndex >= 0) {
      const updatedCustomers = customers.map((customer, index) =>
        index === editingIndex ? { name, email } : customer
      );
      setCustomers(updatedCustomers);
      setEditingIndex(-1);
    } else {
      setCustomers([...customers, { name, email }]);
    }
    setName('');
    setEmail('');
  };

  const editCustomer = (index) => {
    setName(customers[index].name);
    setEmail(customers[index].email);
    setEditingIndex(index);
  };

  const deleteCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        value={name}
        placeholder="Name"
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="email"
        value={email}
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={addOrUpdateCustomer}>
        {editingIndex >= 0 ? 'Update Customer' : 'Add Customer'}
      </button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => editCustomer(index)}>Edit</button>
            <button onClick={() => deleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```