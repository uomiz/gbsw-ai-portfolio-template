document.addEventListener('DOMContentLoaded', () => {
    const projectsGrid = document.getElementById('projects-grid');

    // projects.json 파일 비동기 로드
    fetch('../data/projects.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('네트워크 응답에 문제가 있습니다.');
            }
            return response.json();
        })
        .then(projects => {
            // 로딩 메시지 삭제
            projectsGrid.innerHTML = '';

            // 데이터가 없을 때 처리
            if (projects.length === 0) {
                projectsGrid.innerHTML = '<p>등록된 프로젝트가 없습니다.</p>';
                return;
            }

            // 각 프로젝트 데이터를 순회하며 카드 생성 및 추가
            projects.forEach(project => {
                const card = document.createElement('div');
                card.className = 'project-card';

                // 태그 뱃지 생성
                const tagsHTML = project.tags
                    .map(tag => `<span class="badge">${tag}</span>`)
                    .join('');

                card.innerHTML = `
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div class="tags">${tagsHTML}</div>
                    <a href="${project.link}" target="_blank" class="project-link">자세히 보기 &rarr;</a>
                `;

                projectsGrid.appendChild(card);
            });
        })
        .catch(error => {
            console.error('프로젝트를 불러오는 중 오류 발생:', error);
            projectsGrid.innerHTML = '<p class="error">프로젝트 데이터를 불러오지 못했습니다.</p>';
        });
});