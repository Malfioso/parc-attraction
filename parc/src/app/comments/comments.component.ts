import { Component } from '@angular/core';

interface Comment {
  note: number;
  commentaire: string;
  attraction_id: number;
  users_id: number;
}

@Component({
  selector: 'app-comments',
  standalone: true,
  imports: [],
  templateUrl: './comments.component.html',
  styleUrl: './comments.component.scss',
})
export class CommentsComponent {}
