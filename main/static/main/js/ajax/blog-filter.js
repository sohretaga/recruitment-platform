const url = new URL(window.location);

class DataCollector {

    getBlogCategories() {
        const checkboxes = document.querySelectorAll('#blog-categories input[type="checkbox"]');
        const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
        const selectedValues = selectedCheckboxes.map(checkbox => checkbox.value);
        setUrl('categories', selectedValues.join(','))

        return selectedValues;

    };

    collectData() {
        const data = {
            categories: this.getBlogCategories()
        };

        return data;
    };
};

const toTitleCase = (str) => {
    return str.replace(
      /\w\S*/g,
      function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      }
    );
};

const dateFormat = (date) => {
    const createdDate = new Date(date);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return createdDate.toLocaleDateString('en-US', options);
};

const setUrl = (parameter, value) => {
    const query_parameter = url.searchParams.has(parameter);

    if (value) {
        if (query_parameter) {
            url.searchParams.set(parameter, value);
        } else {
            url.searchParams.append(parameter, value);
        };

    } else {
        url.searchParams.delete(parameter);
    };

    window.history.pushState('', '', decodeURIComponent(url));
};

const getUrlParameterValue = (parameterName) => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const parameterValue = urlParams.get(parameterName);

    return parameterValue;
};

const generatePagination = (paginationInfo) => {
    const container = document.getElementById('pagination-container');
    container.innerHTML = ''; // Clear existing content

    const currentPage = paginationInfo.current_page;
    const numPages = paginationInfo.num_pages;
    const hasPrevious = paginationInfo.has_previous;
    const hasNext = paginationInfo.has_next;
    const separator = url.searchParams.size ? '&':'?'; // return & or ? symbol

    url.hash = ''; // delete #blog-list hash from url
    setUrl('page'); // delete page parameter from url

    // Previous button
    if (hasPrevious) {
        const previousItem = document.createElement('li');
        previousItem.className = 'page-item';
        previousItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${currentPage - 1}#blog-list" tabindex="-1"><i class="mdi mdi-chevron-double-left fs-15"></i></a>`;
        container.appendChild(previousItem);
    };

    // Page numbers
    for (let i = 1; i <= numPages; i++) {
        if (i === 1 || i === numPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${i}#blog-list">${i}</a>`;
            container.appendChild(pageItem);
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            const dotsItem = document.createElement('li');
            dotsItem.className = 'page-item';
            dotsItem.innerHTML = `<a class="page-link" href="${url}#blog-list">...</a>`;
            container.appendChild(dotsItem);
        };
    };

    // Next button
    if (hasNext) {
        const nextItem = document.createElement('li');
        nextItem.className = 'page-item';
        nextItem.innerHTML = `<a class="page-link" href="${url}${separator}page=${currentPage + 1}#blog-list"><i class="mdi mdi-chevron-double-right fs-15"></i></a>`;
        container.appendChild(nextItem);
    };
};

const listBlogs = (blogsInfo) => {
    const container = document.getElementById('blog-list-container');
    container.innerHTML = ''; // Clear existing content

    for (const [key, blog] of Object.entries(blogsInfo)) {
        container.innerHTML += `
        <div class="col-lg-6 mb-4">
            <div class="card blog-grid-box p-2">
                <img src="${blog.cover_photo ? `/media/${blog.cover_photo}`:'/static/main/images/blog/img-05.jpg'}" alt="${toTitleCase(blog.title)}" style="height: 200px;" class="img-fluid">
                <div class="card-body">
                    <ul class="list-inline d-flex justify-content-between mb-3">
                        <li class="list-inline-item">
                            <p class="text-muted mb-0"><a href="#" class="text-muted fw-medium">${blog.category_name ? `${blog.category_name} - `:''}</a>${dateFormat(blog.created_date)}</p>
                        </li>
                        <li class="list-inline-item">
                            <a href="javascript:void(0)" onclick="likeBlog('${blog.id}')">
                                <p class="text-muted mb-0">
                                    <i class="uil uil-thumbs-up ${blog.is_liked ? 'liked':''}" id="like-icon-${blog.id}"></i> <span id="like-count-${blog.id}">${blog.like_count}</span>
                                </p>
                            </a>
                        </li>
                        <li class="list-inline-item">
                            <p class="text-muted mb-0"><i class="mdi mdi-eye"></i> ${blog.views}</p>
                        </li>
                    </ul>
                    <a href="/blog/${blog.slug}" class="primary-link"><h6 class="fs-17">${toTitleCase(blog.title)}</h6></a>
                    <!-- <p class="text-muted">Description</p> -->
                    <div>
                        <a href="/blog/${blog.slug}" class="form-text text-primary">Read More <i class="uil uil-angle-right-b"></i></a>
                    </div>
                </div>
            </div><!--end blog-grid-box-->
        </div>`
    };

};

// Filter Request
const filterRequest = () => {
    const data = new DataCollector();
    const collectded_data = data.collectData();

    $.ajax({
        url: `/blog/ajax/filters`,
        type: 'POST',
        data: JSON.stringify(collectded_data),
        success: (response) => {
            listBlogs(response.blogs);
            generatePagination(response.pagination);
        }

    });
};

const addCheckboxListener = (selector, callback) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', callback);
    });
};

const setFilterCheckboxes = (selector, values) => {
    const checkboxes = document.querySelectorAll(selector);
    checkboxes.forEach(checkbox => {
        if (values.includes(checkbox.value)) {
            checkbox.checked = true;
        };
    });
};

addCheckboxListener('#blog-categories input[type="checkbox"]', filterRequest); // Categories Listener

// Set filter inputs from url parameters
try {
    setFilterCheckboxes('#blog-categories input[type="checkbox"]', getUrlParameterValue('categories').split(',')); // Set categories
} catch (error) { };

const likeBlog = (id) => {
    let likeIcon = document.getElementById(`like-icon-${id}`);
    let likeCount = document.getElementById(`like-count-${id}`);

    $.ajax({
        url: '/blog/ajax/like-blog',
        type: 'POST',
        data: {blog_id: id},
        success: (response) => {
            if (response.action == 'like'){
                likeIcon.classList.add('liked');
                likeCount.innerText = response.count;
            }
            else if(response.action == 'dislike') {
                likeIcon.classList.remove('liked');
                likeCount.innerText = response.count;
            };
        }
    })
}