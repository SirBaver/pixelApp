import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PasswordResetWaitingPage } from './password-reset-waiting.page';

describe('PasswordResetWaitingPage', () => {
  let component: PasswordResetWaitingPage;
  let fixture: ComponentFixture<PasswordResetWaitingPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(PasswordResetWaitingPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
