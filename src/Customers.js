```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');
    const [sortOrder, setSortOrder] = useState('asc');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    const sortedCustomers = [...filteredCustomers].sort((a, b) => {
        return sortOrder === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
    });

    const handleFilterChange = (e) => {
        setFilter(e.target.value);
    };

    const handleSortToggle = () => {
        setSortOrder(prevOrder => (prevOrder === 'asc' ? 'desc' : 'asc'));
    };

    return (
        <div>
            <input type="text" value={filter} onChange={handleFilterChange} placeholder="Filter by name" />
            <button onClick={handleSortToggle}>Sort {sortOrder === 'asc' ? 'Descending' : 'Ascending'}</button>
            <ul>
                {sortedCustomers.map(customer => (
                    <li key={customer.id}>{customer.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```